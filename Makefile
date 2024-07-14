all: data

soundtracks:
	@bash ./download.sh sound

metadata_1.xlsx:
	@bash ./download.sh metadata

metadata_2.xlsx: metadata_1.xlsx

metadata: metadata_2.xlsx

data: soundtracks metadata
	mkdir -p data
	mv soundtracks metadata_* data

.PHONY: clean metadata
clean:
	rm -rf soundtracks
