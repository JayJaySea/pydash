run:
    mkdir -p ./data/icons
    cp -r ./pydash/fonts ./data/
    sassc ./pydash/style/main.scss ./data/style.css
    python ./pydash/scripts/color_icons.py --input-dir pydash/icons --colors pydash/style/colors.scss --output-dir ./data/icons --recolor '#ffffff'
    DEBUG=True python run.py
