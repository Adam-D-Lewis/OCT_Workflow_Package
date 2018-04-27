#pragma once

#ifndef _UT_FFTW_WRAPPER_H_
#define _UT_FFTW_WRAPPER_H_

#include "fftw3.h"
#include <math.h>
#include <vector>
#include <omp.h>
#include <iostream>

#define M_PI 3.14159265358979323846

using namespace std;

class UT_FFTW {
public:
	UT_FFTW();

	int setup_batch(int Length, int N);

	int getLength() { return m_Length_Padded; }

	int execute_batch(float *i_mem, float *o_mem, int Length, int N);

	int cleanup();
private:
	~UT_FFTW();

	bool m_PlanBaked;
	bool m_init;
	int m_Length;
	int m_Length_Padded;
	int m_N;

	float *m_Hanning;

	vector<float> v_IMemory; //In place FFT memory, pre-allocated
	vector<float> v_OMemory; //In place FFT memory, pre-allocated
	fftwf_plan m_FFTWPlans;

	bool checkPlan();
};

//C Interface
extern "C" {
	__declspec(dllexport) int init();
	__declspec(dllexport) int setup_batch(int Length, int N);
	__declspec(dllexport) int execute_batch(float *i_mem, float *o_mem, int Length, int N);
	__declspec(dllexport) int getLength();
	__declspec(dllexport) int cleanup();
	__declspec(dllexport) void preProcess(float *i_mem, float gain, float range, int Length, int N);
	__declspec(dllexport) void postProcess(float *i_mem, int Length, int N);
}

#endif _UT_FFTW_WRAPPER_H_