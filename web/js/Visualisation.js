class Visualisation {

    /**
     * @var {HTMLElement}
     */
    container;

    /**
     * @var {HTMLElement}
     */
    photo_input;

    /**
     * @var {HTMLElement}
     */
    model_input;

    /**
     * @var {HTMLElement}
     */
    photo_button;

    /**
     * @var {HTMLElement}
     */
    model_button;

    /**
     * @param {string} containerSelector
     */
    constructor(containerSelector) {
        this.container = document.querySelector(containerSelector);
        this.init();
    }

    init() {
        this.photo_input = this.container.querySelector('.input-hidden_photo');
        this.model_input = this.container.querySelector('.input-hidden_model');
        this.photo_button = this.container.querySelector('#photo-button');
        this.model_button = this.container.querySelector('#model-button');
        this.preview_photo = this.container.querySelector('.photo-preview__container img');

        initImageLoader();
    }

    initImageLoader() {
        this.photo_button.addEventListener('click', () => {
            this.photo_input.click();
        });

        this.photo_input.addEventListener('change', () => {
            const file = imageInput.files[0];
            const reader = new FileReader();
        
            reader.onload = () => {
                const base64Image = reader.result.split(',')[1];
                eel.loadImage(base64Image)(resizedBase64Image => {
                    // Создаем объект URL для обработанного изображения
                    const resizedImageUrl = `data:image/png;base64,${resizedBase64Image}`;
        
                    // Отображаем обработанное изображение на странице
                    this.preview_photo.src = resizedImageUrl;
                });
            };
        
            reader.readAsDataURL(file);
        });
    }
}