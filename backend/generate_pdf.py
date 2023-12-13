from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas


def create_team_pdf(teams):
    filename = "teams.pdf"

    # Configurar o tamanho do papel para paisagem
    c = canvas.Canvas(filename, pagesize=landscape(letter))

    # Definir posição inicial para as tabelas
    x_position = 50
    y_position = 750

    # Iterar sobre as equipes
    for team in teams:
        # Adicionar o nome da equipe como título
        c.setFont("Helvetica", 12)
        c.drawString(x_position, y_position, f"Team: {team['name']}")

        # Ajustar a posição para a próxima tabela
        y_position -= 20

        # Adicionar cabeçalho da tabela
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_position, y_position, "ID")
        c.drawString(x_position + 40, y_position, "Player Name")

        # Ajustar a posição para os membros da equipe
        y_position -= 20

        # Iterar sobre os jogadores da equipe
        for player in team['players']:
            c.drawString(x_position, y_position, str(player['id']))
            c.drawString(x_position + 40, y_position, player['name'])

            # Ajustar a posição para o próximo jogador
            y_position -= 15

        # Ajustar a posição para a próxima equipe
        y_position -= 20

    # Salvar o PDF
    c.save()
    print(f"PDF gerado com sucesso: {filename}")
