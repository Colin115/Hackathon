from PIL import Image
from pdf417decoder import PDF417Decoder
def get_id_data(file: str):
    # Read the barcode from the specified file
    try:
        image = Image.open("hack.jpeg")
        decoder = PDF417Decoder(image)

        if (decoder.decode() > 0):
            decoded = decoder.barcode_data_index_to_string(0)
            return decoded
    except Exception as e:
        print("Error decoding barcode:", str(e))
        return None

def parse_id_data(data: str):
    user_data = data.split("\n")
    parsed_user_data = {}
    parsed_user_data['lname'] = user_data[2][3:]
    parsed_user_data['fname'] = user_data[4][3:]
    return parsed_user_data