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

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Insufficient arguments detected.");
        return 1;
    }
    else
    {
        long input_file_size;
        int16_t pcm_sample;
        uint16_t adc_sample;
        uint32_t num_of_samples;
        
        char *input_file = argv[1];
        char *output_file = argv[2];

        FILE *fptr_in = fopen(input_file, "rb");
        if (!fptr_in)
        {
            printf("Error in opening input file.");
            return 1;
        }
        else
        {
            // Determine the total size of input file
            fseek(fptr_in, 0, SEEK_END);
            input_file_size = ftell(fptr_in);
            // Move the file pointer to starting point of input file
            fseek(fptr_in, 0, SEEK_SET);
            if (input_file_size % 2 != 0)
            {
                printf("Invalid file size detected.");
                fclose(fptr_in);
                return 1;
            }

            // Write the output file
            num_of_samples = input_file_size / 2;
            FILE *fptr_out = fopen(output_file,"wb");
            if (!fptr_out)
            {
                printf("Error in opening output file.");
                return 1;
            }
            else
            {
                wav_header(fptr_out, num_of_samples);
                for (uint32_t i = 0; i < num_of_samples; ++i)
                {
                    if (fread(&adc_sample, sizeof(uint16_t), 1, fptr_in) != 1)
                    {
                        printf("Error in reading sample.\n");
                        break;
                    }
                    else
                    {
                        pcm_sample = (int16_t) (((int32_t) adc_sample - 2048) * 16);
                        fwrite(&pcm_sample, sizeof(int16_t), 1, fptr_out);
                    }
                }

                fclose(fptr_in);
                fclose(fptr_out);
                
                printf("'%s' WAV file is generated successfully with %u samples.",output_file,num_of_samples);
                return 0;
            }
        }
    }
}