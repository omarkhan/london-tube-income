default: build

data:
	./data.sh

build:
	MINIFY=true cactus build

serve:
	cactus serve
