run:
    mkdir -p ./data/icons
    cp -r ./fonts ./data/
    sassc ./style/main.scss ./data/style.css
    python ./scripts/color_icons.py --input-dir icons --colors style/colors.scss --output-dir ./data/icons --recolor '#ffffff'
    python run.py

