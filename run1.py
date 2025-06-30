import os, cv2, unicodedata
from PIL import Image

list_of_names = []
list_of_matriculas = []
list_of_cursos = []

def delete_old_data():
    for i in os.listdir("generated-certificates/"):
        if i != "pdf":
            os.remove(os.path.join("generated-certificates/", i))
    for i in os.listdir("generated-certificates/pdf"):
        os.remove(os.path.join("generated-certificates/pdf", i))

def cleanup_data():
    with open('name-data.txt', encoding='utf-8') as f:
        for line in f:
            normalized_name = normalizar(line.strip())
            list_of_names.append(normalized_name)
    
    with open('matricula-data.txt', encoding='utf-8') as f:
        for line in f:
            list_of_matriculas.append(line.strip())
    
    with open('curso-data.txt', encoding='utf-8') as f:
        for line in f:
            normalized_curso = normalizar(line.strip())
            list_of_cursos.append(normalized_curso)

def normalizar(text):
    normalized_text = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in normalized_text if not unicodedata.combining(c)])

def generate_certificates():
    for index in range(len(list_of_names)):
        name = list_of_names[index]
        matricula = list_of_matriculas[index]
        curso = list_of_cursos[index]
        
        certificate_template_image = cv2.imread("template.png")
        
        # Cor preta em BGR (OpenCV usa BGR em vez de RGB)
        cor_preta = (0, 0, 0)
        
        # Adiciona nome
        cv2.putText(certificate_template_image, name.strip(), (232, 736), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_preta, 2, cv2.LINE_AA)
        
        # Adiciona matrícula
        cv2.putText(certificate_template_image, matricula.strip(), (912, 736), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_preta, 2, cv2.LINE_AA)
        
        # Adiciona curso
        cv2.putText(certificate_template_image, curso.strip(), (340, 769), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_preta, 2, cv2.LINE_AA)
        
        cv2.imwrite(os.path.join("generated-certificates", f"{name}_2022_1.jpg"), certificate_template_image)
        print("Processando {} / {}".format(index + 1, len(list_of_names)))

    for file in os.listdir("generated-certificates/"):
        if file != "pdf":
            print("Convertendo para pdf:", file)
            if file.split('.')[-1] in ('jpg', 'png'):
                file_name = os.path.basename(file).split('.')[-2]
                normalized_file_name = normalizar(file_name)
                imagem = Image.open(os.path.join("generated-certificates", file))
                imagem_convertida = imagem.convert('RGB')
                imagem_convertida.save(os.path.join("generated-certificates/pdf", f"{normalized_file_name}.pdf"))

def main():
    delete_old_data()
    cleanup_data()
    generate_certificates()

if __name__ == '__main__':
    main()