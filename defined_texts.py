intro = """Du schreibst eine interaktive Geschichte, in der ein Szenario von privat angestellten Hausangestellten mit folgenden Eigenschaften beschrieben wird: \
            - Maximal zwei Charaktere interagieren miteinander\
            - Das Szenario spielt im Kontext der folgenden Tätigkeit: {workArea}
            - Der/die Arbeitgeber*in heißt: {employer}. Über diese Person ist folgendes bekannt: {employerInfo}
            - Der/die Hausangestellte heißt: {employee}. Über diese Person ist folgendes bekannt: {employeeInfo}
            - Die Geschichte ist in folgenden Kontext eingebettet: {outline}
            - Die gleiche Person kann mehrere Textabschnitte hintereinander sagen\
            - Die Geschichte dient zur Weiterbildung der Hausangestellten\
            - Es soll eine runde Geschichte entstehen, die eingeleitet wird und hin zu einem Entscheidungsszenario (Auswahl zwischen drei Möglichkeiten) für die Hausangestellte Person führt\
            - Nach der Entscheidung wird die Geschichte in den Schlussteil geführt\
"""

outline_intro = """
        Ich schreibe interaktive Geschichten mit einem von mir selbst entwickelten Editor. Der Editor \
        ist dafür gedacht, Geschichten zu erstellen in denen zwei Personen interagieren. Der Kontext \
        der Geschichten sind privat angestellte Hausangestellte Hausangestellte wie Reinigungskräfte oder \
        Gärtner. Die Angestellten interagieren aufgrund von unvorhersehbaren oder \
        vorhersehbaren Ereignissen mit dem Arbeitgeber und geraten in eine Situation, in der sie eine \
        schwierige Entscheidung über ihr weiteres Vorgehen treffen müssen. Kannst du für mich \
        ein paar kreative Story-Skizzen für solche interaktiven Geschichten in deutscher Sprache erstellen? \
        
        - Das Szenario spielt im Kontext der folgenden Tätigkeit: {workArea}
        - Der/die Arbeitgeber*in heißt: {employer}. Über diese Person ist folgendes bekannt: {employerInfo}
        - Der/die Hausangestellte heißt: {employee}. Über diese Person ist folgendes bekannt: {employeeInfo}

        Bitte erzeuge einen kreativen Geschichtskontext für eine solche interaktive Geschichte.
"""
