

if __name__ == "__main__":
    import os.path
    import numpy as np
    import matplotlib.pyplot as plt
    import time
    from joblib import Parallel, delayed
    from Pipe_And_Filter_Autosection.classes.FileManager import FileManager as FM

    master_dir_path = os.path.abspath(r'C:\Users\adl628\Desktop\Query Example Data\test')
    num_cores = 2
    def parallel_func(one, two, three):  # , single_build_rises):
        return one + two + three
        # print(f"---file #{i}/{len(N)-1} being processed.")
        # image_stack = np.fromfile(image_stack_path, '>f4').reshape((640, 512, -1), order='F')
        # roi_data = image_stack[282:321, 260:300, :]
        # max_rise = np.mean(np.max(roi_data, axis=2) - roi_data[:, :, 0])
        # # single_build_rises[i] = max_rise

    # with Parallel(n_jobs=num_cores) as parallel:
    #     for i, image_stack_path in enumerate([1, 2, 3]):
    #         val = parallel(delayed(parallel_func)(1, 2, 3))
    # # Parallel(n_jobs=num_cores)(delayed(parallel_func)(1, 2, 3) for _ in [1, 2, 3])


    from joblib import Parallel, delayed
    with Parallel(n_jobs=2) as parallel:
        for val in range(10):
            thing = parallel(delayed(parallel_func)(1, 2, 3) for i in range(1))# for val in range(10))
            print(thing)