INPUT_FILES = [
        "test"
        ]

rule all:
    input:
        expand("{infiles}-ch-utf8.nat", infiles=INPUT_FILES)

rule unzip:
    input:
        "{natfile}.zip"
    output:
        "{natfile}.nat"
    message: "Unziping files..."

    shell:
        "unzip -p {input} > {output}"

rule fixchars:
    input:
        "{natfile}.nat"
    output:
        "{natfile}-ch.nat"
    message:
        "Fixing/deleting chars/lines..."

    run:
        from snakemakeutils import del_char_val, del_char_idx, apply
        trans = [del_char_val('\x00'), del_char_idx(0)]
        apply(trans, "latin1", input, output)

rule utf8_enc:
    input:
        "{natfile}-ch.nat"
    output:
        "{natfile}-ch-utf8.nat"
    message:
        "Recoding from latin1 to UTF-8..."

    shell:
        "iconv -f latin1 -t utf8 -o {output} {input}"



rule clean:
    shell:
        "rm *.nat"

