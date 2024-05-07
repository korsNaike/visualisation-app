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
    method_input;

    /**
     * @var {HTMLElement}
     */
    preview_photo;

    /**
     * @var {HTMLElement}
     */
    result_photo;

    /**
     * @var {HTMLElement}
     */
    submit_button;

    /**
     * @param {string} containerSelector
     * @param {Number} number
     */
    constructor(containerSelector, number = 0) {
        this.container = document.querySelector(containerSelector);
        this.number = number
        this.init();
    }

    init() {
        this.photo_input = this.container.querySelector('.input-hidden_photo');
        this.model_input = this.container.querySelector('.input-hidden_model');
        this.method_input = this.container.querySelector('.input-hidden_method')
        this.photo_button = this.container.querySelector('#photo-button');
        this.preview_photo = this.container.querySelector('.photo-preview__container img');
        this.result_photo = this.container.querySelector('.visualisation-result__img');
        this.submit_button = this.container.querySelector('.input-form__button_submit');
        this.layers_input = this.container.querySelector('#layer-range');

        this.initImageLoader();
        this.initSelect("#model-selector", this.model_input);
        this.initSelect("#method-selector", this.method_input);
        this.initVisualisation();
        this.initListenerToModelInput();
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
                eel.loadImage(base64Image, this.number)(resizedBase64Image => {
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
     * Инициализировать выпадающий список
     * @param {string} selectSelector 
     * @param {HTMLElement} inputForValue 
     */
    initSelect(selectSelector, inputForValue) {
        const optionMenu = this.container.querySelector(selectSelector),
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
                inputForValue.value = selectedOption;
                this.triggerEvent(inputForValue);

                optionMenu.classList.remove("active");
            });
        });
    }

    /**
     * @param {HTMLElement} element 
     * @param {string} type 
     * @param {object} options 
     */
    triggerEvent(element, type = 'change', options = { bubbles: true, cancelable: true }) {
        const event = new Event(type, options);
        element.dispatchEvent(event);
    }

    initListenerToModelInput() {
        this.model_input.addEventListener('change', () => {

            eel.get_available_layers(this.model_input.value)(layers => {
                console.log(layers);

                let countOfLayers = layers.length - 1;
                this.layers_input.setAttribute('max', countOfLayers);

                let copy_layer = this.layers_input.cloneNode(true);
                this.layers_input.parentElement.parentElement.appendChild(copy_layer);
                this.layers_input.parentElement.remove();

                let tick = Math.floor(countOfLayers / 20);
                if (tick == 0) {
                    tick = 1;
                }
                
                let range = new rSlider({
                    element: "#layer-range",
                    tick: tick,
                    data: layers
                });
                this.layers_input = copy_layer;
            })
        })
    }

    initVisualisation() {
        this.submit_button.addEventListener('click', () => {

            const method = this.method_input.value;
            const model = this.model_input.value;

            eel.visualize(model, method, this.number)(data => {
                console.log(data);
                const resizedBase64Image = data.image;

                // Создаем объект URL для обработанного изображения
                const resizedImageUrl = `data:image/png;base64,${resizedBase64Image}`;

                // Отображаем обработанное изображение на странице
                this.result_photo.src = resizedImageUrl;
                this.container.querySelector('.visualisation-text-result').textContent = data.result;
            });
        });
    }
}

const visualisation = new Visualisation('#first-visualisation');