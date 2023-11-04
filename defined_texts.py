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
        Hi ChatGPT, I am writing interactive stories with a custom story editor made by myself. The editor is designed 
        to create stories where two people are interacting. The context of the stories are privately deployed domestic 
        workers such as cleaning persons or gardeners. The employees interact with the employer due to unforeseeable or 
        foreseeable events and get into a situation where they have to make a tough decision how to proceed. Can you 
        give me some creative story outlines for such interactive stories in the German language? \
        
        - Das Szenario spielt im Kontext der folgenden Tätigkeit: {workArea}
        - Der/die Arbeitgeber*in heißt: {employer}. Über diese Person ist folgendes bekannt: {employerInfo}
        - Der/die Hausangestellte heißt: {employee}. Über diese Person ist folgendes bekannt: {employeeInfo}

        Please give me some creative story outlines for such interactive stories in the German language.
"""
