//
//  main.c
//  HeavyPortAudio
//
//  Created by Joe White on 30/07/2015.
//  Copyright (c) 2015 Enzien Audio. All rights reserved.
//

/*
 * This is an example program using Heavy, PortAudio and libsndfile to read
 * the contents of a file, process it through a heavy patch and send it to the
 * output. 
 * 
 * Expected data I/O format here are interleaved short values.
 */

#include <stdio.h>
#include "portaudio.h"
#include "Heavy_Test.h"


// UserData struct to be passed to the audio callback
typedef struct {
  Heavy *hvContext;
} UserData;


// Helper methods
int check_pa_error(int tag, PaError error);

void printHook(double timestampMs, const char *printLabel, const char *msgString, void *userData) {
    printf("[@ %.3fms] %s: %s\n", timestampMs, printLabel, msgString);
}

// Main Audio Processing Callback
static int paCallback(const void *input, void *output,
    unsigned long frameCount, const PaStreamCallbackTimeInfo* timeInfo,
    PaStreamCallbackFlags statusFlags, void *userData)
{
    UserData *data = (UserData *) userData;
    
    short *in = (short *)input;
    short *out = (short *)output;
    
    hv_Test_process_interleaved_short(data->hvContext,
                                              in, out, (int)frameCount);
  return paContinue;
}


int main(int argc, const char * argv[]) {

  UserData data = { NULL };

  const double sampleRate = (double) 44100.0;
  const unsigned long blockSize = 256;

  // Setup PortAudio
  if (check_pa_error(1, Pa_Initialize())) return 1;
  
  // Setup Heavy context
  data.hvContext = hv_Test_new(sampleRate);
  hv_setPrintHook(data.hvContext, &printHook);

  printf("Instantiated heavy context:\n - numInputChannels: %d\n - numOutputChannels: %d\n\n",
      hv_getNumInputChannels(data.hvContext), hv_getNumOutputChannels(data.hvContext));
    
  int inChannels = hv_getNumInputChannels(data.hvContext) ? : 1;
  int outChannels = hv_getNumOutputChannels(data.hvContext) ? : 1;
  
  // Opening stream
  PaStream *stream = NULL;
  if (check_pa_error(2,
      Pa_OpenDefaultStream(&stream, inChannels, outChannels,
          paInt16, sampleRate, blockSize, paCallback, &data))) {
    return 1;
  }

  // Start Processing
  if (check_pa_error(3, Pa_StartStream(stream))) return 1;

  while (Pa_IsStreamActive(stream)) {
    // Pa_Sleep(1000);
  }
  
  // Stop Processing
  if (check_pa_error(5, Pa_CloseStream(stream))) return 1;
  
  // Teardown
  hv_Test_free(data.hvContext);

  if (check_pa_error(7, Pa_Terminate())) return 1;

  printf("Success\n");
  return 0;
}


int check_pa_error(int tag, PaError error) {
  if (error != paNoError) {
    printf("(#%d portaudio error) %s\n", tag, Pa_GetErrorText(error));
    return 1;
  }
  return 0;
}
