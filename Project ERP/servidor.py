import json
import secrets
from http.server import BaseHTTPRequestHandler, HTTPServer
from database import criar_tabelas
from operacoes import inserir_produto, inserir_produtos_lote, editar_produto_completo, listar_produtos, excluir_produto, registrar_movimento, listar_movimentacoes

# ── Usuários cadastrados (para projeto acadêmico) ──
USUARIOS = {
    "admin": "admin123",
    "operador": "op2024"
}

# ── Sessões ativas (token -> usuário) ──
sessoes_ativas = {}


class ServidorNativo(BaseHTTPRequestHandler):

    def _enviar_json(self, dados, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(dados).encode('utf-8'))

    def _enviar_html(self, caminho):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        try:
            with open(caminho, 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.wfile.write(f"Erro: {caminho} nao encontrado.".encode('utf-8'))

    def do_GET(self):
        if self.path == '/':
            self._enviar_html('login.html')

        elif self.path == '/app':
            self._enviar_html('index.html')

        elif self.path == '/api/produtos':
            produtos = listar_produtos()
            resultado = []
            for p in produtos:
                resultado.append({
                    "id": p[0], "nome": p[1], "categoria": p[2], "lote": p[3],
                    "quantidade": p[4], "validade": p[5], "entrada": p[6]
                })
            self._enviar_json(resultado)

        elif self.path == '/api/movimentacoes':
            movimentos = listar_movimentacoes()
            resultado = []
            for m in movimentos:
                resultado.append({
                    "id": m[0], "produto_nome": m[1], "tipo": m[2],
                    "quantidade": m[3], "data_hora": m[4], "motivo": m[5]
                })
            self._enviar_json(resultado)

    def do_POST(self):
        tamanho_conteudo = int(self.headers['Content-Length'])
        dados_post = self.rfile.read(tamanho_conteudo)
        dados = json.loads(dados_post.decode('utf-8'))

        if self.path == '/api/login':
            usuario = dados.get('usuario', '')
            senha = dados.get('senha', '')
            if usuario in USUARIOS and USUARIOS[usuario] == senha:
                token = secrets.token_hex(16)
                sessoes_ativas[token] = usuario
                self._enviar_json({"status": "sucesso", "token": token, "usuario": usuario})
            else:
                self._enviar_json({"status": "erro", "mensagem": "Usuário ou senha incorretos."}, 401)
            return

        elif self.path == '/api/logout':
            token = dados.get('token', '')
            sessoes_ativas.pop(token, None)
            self._enviar_json({"status": "sucesso"})
            return

        elif self.path == '/api/adicionar':
            inserir_produto(dados['nome'], dados['categoria'], dados['lote'], float(dados['quantidade']), dados['validade'], dados['entrada'])
            self._enviar_json({"status": "sucesso"})

        elif self.path == '/api/editar':
            editar_produto_completo(int(dados['id']), dados['nome'], dados['categoria'], dados['lote'], float(dados['quantidade']), dados['validade'], dados['entrada'])
            self._enviar_json({"status": "sucesso"})

        elif self.path == '/api/importar_lote':
            lote = []
            for item in dados:
                lote.append((item['nome'], item['categoria'], item.get('lote', 'Lote Padrão'), float(item['quantidade']), item['validade'], item['entrada']))
            if lote:
                inserir_produtos_lote(lote)
            self._enviar_json({"status": "sucesso", "importados": len(lote)})

        elif self.path == '/api/excluir':
            excluir_produto(int(dados['id']))
            self._enviar_json({"status": "sucesso"})

        elif self.path == '/api/movimentar':
            registrar_movimento(int(dados['id']), dados['tipo'], float(dados['quantidade']), dados['motivo'])
            self._enviar_json({"status": "sucesso"})


def iniciar_servidor():
    criar_tabelas()
    porta = 8080
    servidor = HTTPServer(('', porta), ServidorNativo)
    print(f"Servidor ERP Ativo: http://localhost:{porta}")
    print(f"Usuarios disponiveis: {', '.join(USUARIOS.keys())}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    servidor.server_close()


if __name__ == '__main__':
    iniciar_servidor()