import sqlite3

class Aluno:
    @staticmethod
    def buscar_disciplinas(aluno_id):
        """
        Busca as disciplinas cursadas pelo aluno.
        Retorna uma lista de tuplas contendo (nome_da_disciplina, nome_do_professor, id_da_disciplina).
        """
        conn = sqlite3.connect("extensao.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT d.nome, u.nome_completo, d.id
        FROM disciplinas d
        JOIN usuarios u ON d.professor_id = u.id
        WHERE d.id IN (
            SELECT disciplina_id FROM frequencias WHERE aluno_id=?
        )
        ''', (aluno_id,))
        disciplinas = cursor.fetchall()
        conn.close()
        return disciplinas

    @staticmethod
    def buscar_frequencia(aluno_id, disciplina_id):
        """
        Calcula a frequência do aluno em uma disciplina.
        Retorna a frequência como uma porcentagem (ex.: 85.71%).
        """
        conn = sqlite3.connect("extensao.db")
        cursor = conn.cursor()

        # Conta o número total de presenças
        cursor.execute('''
        SELECT COUNT(*) AS total_presencas
        FROM frequencias
        WHERE aluno_id=? AND disciplina_id=? AND presente=1
        ''', (aluno_id, disciplina_id))
        presencas = cursor.fetchone()[0]

        # Conta o número total de aulas
        cursor.execute('''
        SELECT COUNT(*) AS total_aulas
        FROM frequencias
        WHERE aluno_id=? AND disciplina_id=?
        ''', (aluno_id, disciplina_id))
        total_aulas = cursor.fetchone()[0]

        conn.close()

        # Se não houver aulas registradas, a frequência é 0%
        if total_aulas == 0:
            return 0

        # Calcula a frequência como uma porcentagem
        return round((presencas / total_aulas) * 100, 2)

    @staticmethod
    def buscar_nota(aluno_id, disciplina_id):
        """
        Calcula a média das notas do aluno em uma disciplina.
        Retorna a média arredondada para uma casa decimal ou "N/A" se não houver notas.
        """
        conn = sqlite3.connect("extensao.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT AVG(valor_nota) AS media
        FROM notas
        WHERE aluno_id=? AND disciplina_id=?
        ''', (aluno_id, disciplina_id))
        nota = cursor.fetchone()[0]
        conn.close()

        if nota is not None:
            return round(nota, 1)
        return "N/A"

    @staticmethod
    def buscar_notas_por_tipo(aluno_id, disciplina_id):
        """
        Busca as notas do aluno separadas por tipo de avaliação (AV1, AV2, AVS).
        Retorna um dicionário com as notas por tipo.
        """
        conn = sqlite3.connect("extensao.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT a.tipo_avaliacao, n.valor_nota
        FROM notas n
        JOIN avaliacoes a ON n.avaliacao_id = a.id
        WHERE n.aluno_id=? AND n.disciplina_id=?
        ''', (aluno_id, disciplina_id))
        notas = cursor.fetchall()
        conn.close()

        # Organiza as notas por tipo de avaliação
        notas_por_tipo = {"AV1": "N/A", "AV2": "N/A", "AVS": "N/A"}
        for tipo, valor in notas:
            if tipo in notas_por_tipo:
                notas_por_tipo[tipo] = round(valor, 1) if valor is not None else "N/A"
        return notas_por_tipo

    @staticmethod
    def buscar_avaliacoes(aluno_id):
        """
        Busca as próximas avaliações do aluno.
        Retorna uma lista de tuplas contendo (nome_da_disciplina, data_da_avaliacao, descricao, tipo_avaliacao).
        """
        conn = sqlite3.connect("extensao.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT d.nome, a.data_avaliacao, a.descricao, a.tipo_avaliacao
        FROM avaliacoes a
        JOIN disciplinas d ON a.disciplina_id = d.id
        WHERE d.id IN (
            SELECT disciplina_id FROM frequencias WHERE aluno_id=?
        ) AND a.data_avaliacao >= DATE('now')
        ORDER BY a.data_avaliacao ASC
        ''', (aluno_id,))
        avaliacoes = cursor.fetchall()
        conn.close()
        return avaliacoes