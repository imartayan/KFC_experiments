#include <stdlib.h>
#include <stdio.h>
#include <zlib.h>
#include <assert.h>

#include "kseq.h"
#include "ketopt.h"

KSEQ_INIT(gzFile, gzread)

typedef enum {
    OK,
    ERR_FILE,
    ERR_OUTOFBOUNDS,
    ERR_OPTION,
    ERR_RUNTIME
} error_t;

void print_help() {
    fprintf(stderr, "[sample file by coverage] options:\n");
    fprintf(stderr, "\t-i\tinput fasta file [stdin]\n");
    fprintf(stderr, "\t-o\toutput file [stdout].\n");
    fprintf(stderr, "\t-c\ttarget coverage\n");
    fprintf(stderr, "\t-s\tgenome size\n");
    fprintf(stderr, "\t-h\tshow this help\n");
}

int print_string(FILE* stream, char* str, size_t size) {
    if (fwrite(str, 1, size, stream) != size) return ERR_RUNTIME;
    return OK;
}

int main(int argc, char** argv) {
    gzFile fp;
    FILE *oh;
    kseq_t *seq;
    unsigned long long coverage, genome_length, bases_read, threshold;
    ketopt_t opt;
    long long parsed;
    int c, err;
    
    assert(argv);

    fp = NULL;
    oh = NULL;
    seq = NULL;
    coverage = 0;
    genome_length = 0;
    c = 0;
    err = OK;

    opt = KETOPT_INIT;
    static ko_longopt_t longopts[] = {{NULL, 0, 0}};

    while((c = ketopt(&opt, argc, argv, 1, "i:o:c:s:h", longopts)) >= 0) {
        if (c == 'i') {
            if ((fp = gzopen(opt.arg, "r")) == NULL) {
                fprintf(stderr, "Unable to open the input file %s\n", opt.arg);
                return ERR_FILE;
            }
        } else if (c == 'o') {
            if ((oh = fopen(opt.arg, "w")) == NULL) {
                fprintf(stderr, "Unable to create output file %s\n", opt.arg);
                return ERR_FILE;
            }
        } else if (c == 'c') {
            parsed = strtol(opt.arg, NULL, 10);
            if (parsed > (unsigned long)-1) {
                fprintf(stderr, "Unable to parse coverage\n");
                return ERR_OUTOFBOUNDS;
            }
            coverage = (unsigned long long)parsed;
        } else if (c == 's') {
            parsed = strtol(opt.arg, NULL, 10);
            if (parsed > (unsigned long)-1) {
                fprintf(stderr, "Unable to parse genome size\n");
                return ERR_OUTOFBOUNDS;
            }
            genome_length = (unsigned long long)parsed;
        } else if (c == 'h') {
            print_help();
            return OK;
        } else {
            fprintf(stderr, "Option -%c not available\n", c);
            return ERR_OPTION;
        }
    }

    if (fp == NULL) {
        if ((fp = gzdopen(fileno(stdin), "r")) == NULL) {
            fprintf(stderr, "Unable to use stdin as input\n");
            return ERR_OPTION;
        }
    }
    if (oh == NULL) {
        oh = stdout;
    }
    seq = kseq_init(fp);
    assert(seq);
    threshold = coverage * genome_length;
    bases_read = 0;
    while(err == OK && bases_read < threshold && kseq_read(seq) >= 0) {
        fprintf(stderr, "read sequence of length %zu\n", seq->seq.l);
        bases_read += seq->seq.l;
        {
            fprintf(oh, ">");
            print_string(oh, seq->name.s, seq->name.l);
            fprintf(oh, "\n");
            print_string(oh, seq->seq.s, seq->seq.l);
            fprintf(oh, "\n");
        }
    }
    return 0;
}