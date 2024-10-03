import os, cv2, unicodedata
from PIL import Image

list_of_names = []

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

def normalizar(text):
    normalized_text = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in normalized_text if not unicodedata.combining(c)])

def generate_certificates():
    for index, name in enumerate(list_of_names):
        certificate_template_image = cv2.imread("template.png")
        cv2.putText(certificate_template_image, name.strip(), (570, 588), cv2.FONT_HERSHEY_SIMPLEX, 2, (82, 18, 8), 2, cv2.LINE_AA)
        cv2.imwrite(os.path.join("generated-certificates", f"{name}.jpg"), certificate_template_image)
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