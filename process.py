import uuid
import sys
import json
import base64

def encode_images_to_files(display_data_json):
    # sys.stderr.write("encoding\n")
    if display_data_json.get("output_type", None) == "display_data":
        metadata = display_data_json.get("metadata")
        data = display_data_json.get("data")
        if data.has_key("image/png"):
            if not metadata.has_key("image/png"):
                metadata["image/png"] = {}
            if not metadata.get("image/png").has_key("location"):
                metadata["image/png"]["location"] = "images/auto_" + uuid.uuid4().hex + ".png"
                sys.stderr.write("git add {}\n".format(metadata["image/png"]["location"]))
            location = metadata.get("image/png").get("location")
            with open(location, 'wb') as fout:
                # remove from data and write to the file
                fout.write(base64.b64decode(data.pop("image/png")))
        display_data_json["metadata"] = metadata
        display_data_json["data"] = data
    return display_data_json

def decode_images_from_files(display_data_json):
    # sys.stderr.write("decoding\n")
    if display_data_json.get("output_type", None) == "display_data":
        metadata = display_data_json.get("metadata")
        data = display_data_json.get("data")
        if metadata.has_key("image/png"):
            if not data.has_key("image/png") and metadata["image/png"].has_key("location"):
                location = metadata.get("image/png").get("location")
                with open(location, 'rb') as fin:
                    data["image/png"] = fin.read().encode('base64')
        display_data_json["metadata"] = metadata
        display_data_json["data"] = data
    return display_data_json

def main(images_to_files):
    if images_to_files == 'encode':
        hook = encode_images_to_files
        sys.stderr.write("encoding\n")
    elif images_to_files == 'decode':
        hook = decode_images_from_files
        sys.stderr.write("decoding\n")

    sys.stderr.write("reading\n")
    outstream = json.load(sys.stdin, object_hook=hook)
    sys.stderr.write("writing\n")
    json.dump(outstream, sys.stdout, indent=2, sort_keys=True)

if __name__ == '__main__':
    main(*sys.argv[1:])
