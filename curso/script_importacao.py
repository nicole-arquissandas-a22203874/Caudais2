from curso.models import*
import json

Curso.objects.all().delete()
Disciplina.objects.all().delete()

def importar_curso(ficheiro_json):
    with open(f'curso/jsons/{ficheiro_json}') as f:
        data = json.load(f)
        informacaoCurso=data['courseDetail']
        disciplinas=data['courseFlatPlan']

        Curso.objects.create(
            nome=informacaoCurso['courseName'],
            apresentacao=informacaoCurso['presentation'],
            objetivos=informacaoCurso['objectives'],
            competencias=informacaoCurso['competences']

            )
        for disciplina in disciplinas:
            Disciplina.objects.create(
                nome=disciplina['curricularUnitName'],
                ano=disciplina['curricularYear'],
                semestre=disciplina['semester'],
                ects=disciplina['ects'],
                curricularIUnitReadableCode=disciplina['curricularIUnitReadableCode']
            )



