#include "UT_FFTW_Wrapper.h"
#include <cassert>
#include <chrono>

int main() {
	int length = 4096;
	int N = 10000;
	int AvgCount = 10;

	float *i_mem = new float[length*N];
	
	init();
	setup_batch(length, N);
	
	int padded_length = getLength();
	float *o_mem = new float[padded_length*N];

	auto timeInMs = 0;
	for (int i = 0; i < AvgCount; i++) {
		auto t1 = std::chrono::high_resolution_clock::now();
		//preProcess(i_mem, 4 / pow(2, 16), 2, length, N);
		execute_batch(i_mem, o_mem, length, N);
		//postProcess(o_mem, getLength(), N);
		auto t2 = std::chrono::high_resolution_clock::now();

		timeInMs += std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();
	}

	auto avgTime = timeInMs / AvgCount;

	cout << "Average Time to run : " << avgTime << " ms \r";
	int x;
	cin >> x;
}