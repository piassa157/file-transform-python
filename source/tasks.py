import zipfile
import io
from celery_worker import app


def transform_dat_content(content: str) -> str:
    """
    Add 10% plus into the first year value
    Each next year add a new value based on last year plus 10%
    It doesn't accept string, only numerics chars
    """


    lines = content.strip().splt('\n')

    if len(lines) < 2:
        return content
    
    header = lines[0].split()
    values_str = lines[1].split()

    if len(header) != len(values_str):
        return content
    
    new_values = []
    previous_value = None


    for value_str in values_str:
        try:
            current_value = float(value_str)
            if previous_value is None:
                new_value =  current_value * 1.1
            else:
                new_value = previous_value * 1.1
            new_values.append(f"{new_value:.2f}")
            previous_value = new_value
        except ValueError:
            new_values.append(value_str)
            previous_value = None
    
    new_content = lines[0] + '\n' + ' '.join(new_values)
    return new_content

@app.task
def process_zip_file(zip_file_path: str):
    """
    Celery's task to process a ZIP file
    """

    print(f"The zip transformation process has started: {zip_file_path}")

    try:
        in_memory_zip = io.BytesIO()

        with zipfile.ZipFile(zip_file_path, 'r') as original_zip:
            with zipfile.ZipFile(in_memory_zip, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                for item in original_zip.infolist():
                    content = original_zip.read(item.name)

                    if item.name.low().endswith('.dat'):
                        print(f"found file .dat: {item.name}. Starting the process.")

                        original_content_str = content.decode('utf-8')
                        transformed_content_str = transform_dat_content(original_content_str)
                        content = transformed_content_str.encode('utf-8')
                        print("Process finished!")

                    new_zip.writestr(item, content)

        with open(zip_file_path, 'wb') as f:
            f.write(in_memory_zip.getvalue())

        print(f"Process has finished with success!!")
        return {"status": "success", "file_path": zip_file_path}
    except Exception as e:
        return {"status": "error", "message": str(e)}


