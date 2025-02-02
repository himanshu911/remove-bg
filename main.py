import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from rembg import remove
from PIL import Image
from io import BytesIO

app = FastAPI()
templates = Jinja2Templates(
    directory="templates"
)  # Ensure your index.html is in the 'templates' folder


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def remove_background(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        # Open the uploaded image using Pillow
        input_image = Image.open(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Remove the background (using rembg)
    output_image = remove(input_image, post_process_mask=True)

    # Save the output image into an in-memory buffer
    img_io = BytesIO()
    output_image.save(img_io, format="PNG")
    img_io.seek(0)

    # Construct a new filename using the original filename with '_rmbg.png' appended.
    original_filename = file.filename
    basename, _ = os.path.splitext(original_filename)
    new_filename = f"{basename}_rmbg.png"

    # Return the processed image as a downloadable file.
    return StreamingResponse(
        img_io,
        media_type="image/png",
        headers={"Content-Disposition": f'attachment; filename="{new_filename}"'},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5100, reload=True)
