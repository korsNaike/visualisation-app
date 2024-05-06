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
     * @var {HTMLElement}
     */
    preview_photo;

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
        this.submit_button = this.container.querySelector('.input-form__button_submit');

        this.initImageLoader();
        this.initSelectorModel();
        this.initVisualisation();
    }

    /**
     * Инициализация загрузчика изображений
     */
    initImageLoader() {
        this.photo_button.addEventListener('click', () => {
            this.photo_input.click();
        });

        this.photo_input.addEventListener('change', () => {
            const file = this.photo_input.files[0];
            const reader = new FileReader();

            reader.onload = () => {
                const base64Image = reader.result.split(',')[1];
                eel.loadImage(base64Image)(resizedBase64Image => {
                    // Создаем объект URL для обработанного изображения
                    const resizedImageUrl = `data:image/png;base64,${resizedBase64Image}`;

                    // Отображаем обработанное изображение на странице
                    this.preview_photo.src = resizedImageUrl;
                    this.photo_button.querySelector('.plus-icon').innerText = '✓'
                    this.photo_button.querySelector('.button-text').innerText = 'Фото загружено'
                });
            };

            reader.readAsDataURL(file);
        });
    }

    /**
     * Инизиализация выборки модели из выпадающего списка
     */
    initSelectorModel() {
        const optionMenu = this.container.querySelector(".select-menu"),
            selectBtn = optionMenu.querySelector(".select-btn"),
            options = optionMenu.querySelectorAll(".option"),
            sBtn_text = optionMenu.querySelector(".sBtn-text");

        selectBtn.addEventListener("click", () =>
            optionMenu.classList.toggle("active")
        );

        options.forEach((option) => {
            option.addEventListener("click", () => {
                let selectedOption = option.querySelector(".option-text").innerText;
                let textElement = document.createElement('span');
                textElement.classList.add('button-text');
                textElement.style.paddingTop = '0.5rem';
                textElement.style.paddingBottom = '0.5rem';
                textElement.innerText = selectedOption;

                sBtn_text.innerHTML = textElement.outerHTML;
                this.model_input.value = selectedOption;

                optionMenu.classList.remove("active");
            });
        });
    }

    initVisualisation() {
        this.submit_button.addEventListener('click', () => {
            eel.visualize()(resizedBase64Image => {
                // Создаем объект URL для обработанного изображения
                const resizedImageUrl = `data:image/png;base64,${resizedBase64Image}`;

                // Отображаем обработанное изображение на странице
                this.preview_photo.src = resizedImageUrl;
                this.photo_button.querySelector('.plus-icon').innerText = '--------'
                this.photo_button.querySelector('.button-text').innerText = 'ФЛЕКС'
            });
        });
    }
}

const visualisation = new Visualisation('#first-visualisation');