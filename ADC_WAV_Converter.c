#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

void wav_header(FILE *output_file_arg, uint32_t num_of_samples_arg)
{
    uint16_t bits_per_sample = 16;
    uint16_t num_of_channels = 1;
    uint32_t sample_rate = 6400;
    uint32_t data_size = num_of_samples_arg * num_of_channels * bits_per_sample / 8;
    uint32_t file_size = 36 + data_size;
    uint32_t format_length = 16;
    uint16_t audio_format = 1;
    uint32_t bytes_per_second = sample_rate * num_of_channels * bits_per_sample / 8;
    uint16_t bytes_per_channel = num_of_channels * bits_per_sample / 8;

    fwrite("RIFF", 1, 4, output_file_arg);              // "RIFF" file type
    fwrite(&file_size, 4, 1, output_file_arg);          // Total size of file (in bytes) - with header information
    fwrite("WAVE", 1, 4, output_file_arg);              // "WAV" file type
    fwrite("fmt ", 1, 4, output_file_arg);              // Format chunk marker
    fwrite(&format_length, 4, 1, output_file_arg);      // Length of format data
    fwrite(&audio_format, 2, 1, output_file_arg);       // Audio format
    fwrite(&num_of_channels, 2, 1, output_file_arg);    // Number of audio channels
    fwrite(&sample_rate, 4, 1, output_file_arg);        // Sampling rate of saved audio (in samples/second)
    fwrite(&bytes_per_second, 4, 1, output_file_arg);   // (in bytes/second) 
    fwrite(&bytes_per_channel, 2, 1, output_file_arg);  // (in bytes/channel)
    fwrite(&bits_per_sample, 2, 1, output_file_arg);    // (in bits/sample)
    fwrite("data", 1, 4, output_file_arg);              // Data chunk header
    fwrite(&data_size, 4, 1, output_file_arg);          // Total size of data (in bytes) - without header information
}

