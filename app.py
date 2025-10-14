from flask import (
    Flask,
    request,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    Response,
    jsonify,
)
import time
import cv2
from functools import wraps

from services.manipular_database import criar_usuario, verificar_login
from utils.validacoes import (
    validar_email,
    validar_senha,
    validar_username,
    validar_telefone,
)

from utils.manipular_forms import obter_dados_login, obter_dados_cadastro

app = Flask(__name__)
app.secret_key = "d2ccd1731dc1cca262d6c889e3352a921f973db9698cc4ba"

# Variável global para a captura de vídeo do OpenCV
camera = None
selected_camera_index = 0


def login_required(f):
    """
    Decorator que verifica se o usuário está logado.
    Se não estiver, redireciona para a página unauthorized.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('unauthorized'))
        return f(*args, **kwargs)
    return decorated_function


def detect_available_cameras():
    """Detecta todas as câmeras disponíveis no sistema."""
    available_cameras = []

    # Testa até 10 portas de câmera (geralmente suficiente)
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # Tenta ler um frame para confirmar que a câmera funciona
            ret, frame = cap.read()
            if ret:
                available_cameras.append(
                    {
                        "index": i,
                        "name": f"Câmera {i}",
                        "resolution": f"{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}",
                    }
                )
                print(f"Câmera encontrada na porta {i}")
            cap.release()

    return available_cameras


def get_camera():
    """Tenta inicializar a câmera do OpenCV de forma segura."""
    global camera, selected_camera_index
    if camera is None or not camera.isOpened():
        # Usa o índice selecionado pelo usuário
        new_camera = cv2.VideoCapture(selected_camera_index)

        if new_camera.isOpened():
            camera = new_camera
            print(f"Câmera {selected_camera_index} conectada com sucesso.")
        else:
            print(f"Erro: Não foi possível acessar a câmera {selected_camera_index}.")
    return camera


def generate_frames():
    """Gera frames de vídeo em formato JPEG para streaming."""
    global camera

    if camera is None or not camera.isOpened():
        print("Câmera indisponível para streaming.")
        # Gera um frame de erro
        error_frame = create_error_frame("Câmera não conectada")
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + error_frame + b"\r\n")
        return

    frame_count = 0
    while True:
        try:
            # Lê o frame da câmera
            success, frame = camera.read()
            if not success:
                print("Erro ao ler frame da câmera.")
                frame_count += 1
                if frame_count > 10:  # Se falhar muitas vezes, para o loop
                    break
                continue

            # Reset contador se frame foi lido com sucesso
            frame_count = 0

            # Codifica o frame para o formato JPEG
            ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not ret:
                print("Erro ao codificar frame.")
                continue

            # Converte o buffer em bytes e gera o frame no formato multi-part
            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )

        except Exception as e:
            print(f"Erro no streaming: {e}")
            break

        # Adiciona um pequeno atraso para controlar a taxa de frames
        time.sleep(0.03)  # ~30 FPS


def create_error_frame(message):
    """Cria um frame de erro com texto."""
    import numpy as np

    # Cria uma imagem preta
    frame = np.zeros((480, 640, 3), dtype=np.uint8)

    # Adiciona texto de erro
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 255, 255)  # Branco
    thickness = 2

    # Calcula posição do texto para centralizar
    text_size = cv2.getTextSize(message, font, font_scale, thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = (frame.shape[0] + text_size[1]) // 2

    cv2.putText(frame, message, (text_x, text_y), font, font_scale, color, thickness)

    # Codifica para JPEG
    ret, buffer = cv2.imencode(".jpg", frame)
    return buffer.tobytes()


# Rota para o streaming de vídeo
@app.route("/video_feed")
def video_feed():
    """Retorna o stream de vídeo em um formato multi-part para o navegador."""
    # O mimetype 'multipart/x-mixed-replace' é essencial para streaming contínuo.
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# Rota para listar câmeras disponíveis
@app.route("/cameras/list", methods=["GET"])
def list_cameras():
    """Lista todas as câmeras disponíveis no sistema."""
    try:
        cameras = detect_available_cameras()
        return jsonify({"success": True, "cameras": cameras, "count": len(cameras)})
    except Exception as e:
        return jsonify(
            {"success": False, "message": f"Erro ao detectar câmeras: {str(e)}"}
        )


# Rota para controlar a conexão da câmera
@app.route("/camera/status", methods=["GET"])
def camera_status():
    """Retorna o status atual da câmera."""
    global camera, selected_camera_index
    if camera is not None and camera.isOpened():
        return jsonify(
            {
                "status": "connected",
                "message": "Câmera conectada",
                "camera_index": selected_camera_index,
            }
        )
    else:
        return jsonify(
            {
                "status": "disconnected",
                "message": "Câmera desconectada",
                "camera_index": selected_camera_index,
            }
        )


# Rota para conectar/desconectar a câmera
@app.route("/camera/connect", methods=["POST"])
def connect_camera():
    """Conecta a câmera."""
    global camera, selected_camera_index

    try:
        # Obtém o índice da câmera do JSON da requisição
        data = request.get_json()
        camera_index = data.get("camera_index", 0) if data else 0

        # Desconecta câmera atual se estiver conectada
        if camera is not None:
            camera.release()
            camera = None

        # Tenta conectar à câmera selecionada
        camera = cv2.VideoCapture(camera_index)

        if camera.isOpened():
            selected_camera_index = camera_index
            return jsonify(
                {
                    "success": True,
                    "message": f"Câmera {camera_index} conectada com sucesso",
                    "camera_index": camera_index,
                }
            )
        else:
            return jsonify(
                {
                    "success": False,
                    "message": f"Não foi possível conectar à câmera {camera_index}",
                }
            )
    except Exception as e:
        return jsonify(
            {"success": False, "message": f"Erro ao conectar câmera: {str(e)}"}
        )


@app.route("/camera/disconnect", methods=["POST"])
def disconnect_camera():
    """Desconecta a câmera."""
    global camera
    try:
        if camera is not None:
            camera.release()
            camera = None
        return jsonify({"success": True, "message": "Câmera desconectada com sucesso"})
    except Exception as e:
        return jsonify(
            {"success": False, "message": f"Erro ao desconectar câmera: {str(e)}"}
        )


# Rota principal: Tela de login
@app.route("/", methods=["GET", "POST"])
def tela_login():
    validacao = False  # Inicializa a variável de validação como False
    dados_usuario_bd = None  # Inicializa a variável de dados do usuário como None

    if request.method == "POST":
        # Obtém os dados do formulário
        usuario, senha = obter_dados_login(request.form)

        # Chama a função verificar_login para validar o login
        dados_usuario_bd = verificar_login(usuario, senha)

        if dados_usuario_bd:
            validacao = True
            session["usuario"] = dados_usuario_bd
            return redirect(url_for("dashboard"))

        else:
            validacao = False

    return render_template(
        "index.html", validacao=validacao, dados_usuario_bd=dados_usuario_bd
    )


@app.route("/cadastro", methods=["GET", "POST"])
def tela_cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")

    elif request.method == "POST":
        # 1. Obtém dados do formulário
        c_usuario, c_email, c_telefone, c_senha = obter_dados_cadastro(request.form)
        erro = False 

        # Exemplo de lógica de validação:
        if not validar_username(c_usuario):
            flash("Nome de usuário inválido.", "erro")
            erro = True

        if erro:
            dados_para_manter = (c_usuario, c_email, c_telefone, c_senha)
            return render_template("cadastro.html", user_data=dados_para_manter)
        else:
            criar_usuario((c_usuario, c_email, c_telefone, c_senha))
            flash("Conta criada com sucesso! Faça login abaixo.", "sucesso")
            return redirect(url_for("tela_login"))

    return redirect(url_for("tela_login"))


@app.route("/dashboard")
@login_required
def dashboard():
    # O streaming de vídeo será puxado pela rota /video_feed
    return render_template("dashboard.html")


@app.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")


if __name__ == "__main__":
    app.run(debug=True)
    # Garante que a câmera seja liberada ao fechar o app
    if camera is not None:
        camera.release()
