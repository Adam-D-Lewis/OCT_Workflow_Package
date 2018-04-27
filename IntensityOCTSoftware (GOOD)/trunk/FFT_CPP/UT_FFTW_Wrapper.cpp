#include "UT_FFTW_Wrapper.h"

UT_FFTW *global_UT_FFTW;
vector<float> g_Hanning;

UT_FFTW::UT_FFTW() {
	//int check = fftw_init_threads();

	m_PlanBaked = false;
	m_Length = -1;
	m_N = -1;
	m_init = true;
}

UT_FFTW::~UT_FFTW() {

}

int UT_FFTW::cleanup() {
	try {
		fftwf_destroy_plan(m_FFTWPlans);
		v_IMemory.clear();
		v_OMemory.clear();
		return 0;
	}
	catch (...) {
		return 1;
	}

}

//Checks if the FFTW plan is valid or not
//Not fool proof, just a check
bool UT_FFTW::checkPlan() {
	if (m_Length <= 0) {
		return false;
	}

	if (m_N <= 0) {
		return false;
	}

	if (m_PlanBaked == false) {
		return false;
	}

	if (m_init == false) {
		return false;
	}

	return true;
}

int UT_FFTW::execute_batch(float *i_mem, float *o_mem, int Length, int N) {	
	if (Length != m_Length && N != m_N) {
		setup_batch(Length, N);
	}
	
	omp_set_num_threads(2);

	if (checkPlan()) {
#pragma omp parallel for
		for (int i = 0; i < m_N; i++) {
			float *i_ptr = &i_mem[i*m_Length];
			float *o_ptr = &o_mem[i*m_Length_Padded];

			fftwf_execute_dft_r2c(m_FFTWPlans, i_ptr, (fftwf_complex*)o_ptr);
		}

		return 0;
	}
	else {
		return 5;
	}
}

int UT_FFTW::setup_batch(int Length, int N) {
	try {
		m_PlanBaked = false;

		m_Length = Length;
		m_N = N;

		//compute nearest pow 2 or pow 3, this is for zero padding and inplace FFT, as called for in FFTW
		//"For an in-place transform, it is important to remember that the real array will require padding" -http://www.fftw.org/doc/Real_002ddata-DFTs.html#Real_002ddata-DFTs
		m_Length_Padded = m_Length;
		m_Length_Padded = 2 * (m_Length_Padded / 2 + 1);

		v_IMemory = vector<float>(m_Length*m_N);
		v_OMemory = vector<float>(m_Length_Padded*m_N);

		//fftw_plan_with_nthreads(2);
		m_FFTWPlans = fftwf_plan_dft_r2c_1d(m_Length_Padded, v_IMemory.data(), (fftwf_complex*)v_OMemory.data(), FFTW_MEASURE);
		
		int n[] = { m_Length };
		int input_length[] = { m_Length };
		int output_length[] = { m_Length_Padded };
		
		//m_FFTWPlans = 
			//fftwf_plan_many_dft_r2c(1, n, m_N, v_IMemory.data(), input_length, 1, m_N, (fftwf_complex*)v_OMemory.data(), output_length, 1, m_N, FFTW_MEASURE);

		m_PlanBaked = true;

		return 0;
	}
	catch (...) {
		return 6;
	}
}


//***********C Interface****************
__declspec(dllexport) int init() {
	int success = 10;
	try {
		global_UT_FFTW = new UT_FFTW();
		success = 0;
	}
	catch(...){
		success = 10;
	}
	return success;
}

__declspec(dllexport) int setup_batch(int Length, int N) {
	return global_UT_FFTW->setup_batch(Length, N);
}

__declspec(dllexport) int execute_batch(float *i_mem, float *o_mem, int Length, int N) {
	return global_UT_FFTW->execute_batch(i_mem, o_mem, Length, N);
}

__declspec(dllexport) void preProcess(float *i_mem, float gain, float range, int Length, int N) {
	if (g_Hanning.size() != Length) {
		g_Hanning.resize(Length);
		for (int i = 0; i < Length; i++) {
			float tmp = .5*(1 - cos(2 * M_PI*i / Length));
		}
	}
	
	for (int i = 0; i < N; i++) {
		for (int k = 0; k < Length; k++) {
			float tmp = i_mem[k + i*Length];
			tmp = ((tmp - 32768)*gain - range)*g_Hanning.at(k);
		}
	}
}

__declspec(dllexport) void postProcess(float *i_mem, int Length, int N) {
	for (int i = 0; i < N; i++) {
		for (int k = 0; k < Length/2; k++) {
			float r = i_mem[(2*k) + i*Length];
			float j = i_mem[(2*k + 1) + i*Length];
			float out = pow(j, 2) + pow(r, 2);
			out = 20 * log10f(out);
		}
	}
}

__declspec(dllexport) int getLength() {
	return global_UT_FFTW->getLength();
}

__declspec(dllexport) int cleanup() {
	return global_UT_FFTW->cleanup();
}
