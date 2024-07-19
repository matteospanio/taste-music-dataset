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
	bash ./handle_env.sh
	mkdir -p data/dataset
	mv data/soundtracks/* data/dataset
	mv data/annotations/* data/dataset

.PHONY: clean metadata
clean:
	rm -rf soundtracks
