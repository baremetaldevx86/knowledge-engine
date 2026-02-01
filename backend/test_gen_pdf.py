from reportlab.pdfgen import canvas

def create_pdf(filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "The Kronig-Penney model describes the behavior of electrons in a periodic potential.")
    c.drawString(100, 730, "It is essential for understanding band theory in solids.")
    c.save()

if __name__ == "__main__":
    create_pdf("test_upload.pdf")
    print("Created test_upload.pdf")
