import numpy as np
from scipy.io import wavfile
import scipy.io.wavfile as wavf
from pydub import AudioSegment
from tqdm import tqdm

def lpf ( dB, Fc, Fs, X) :
	A = B = C = D = 0
	Y_array = []

	K = ((2*Fs - 2*np.pi*Fc)/(2*Fs + 2*np.pi*Fc))**2
	L = (4*Fs - 4*np.pi*Fc)/(2*Fs + 2*np.pi*Fc)
	M = ((2*np.pi*Fc)/(2*Fs + 2*np.pi*Fc))**2

	gain = 10**(dB/20)

	for term in tqdm(X, unit =" sample", desc ="Low Passing... "):
		Y = gain*M*term + 2*gain*M*A + gain*M*B + L*C - K*D
		Y_array.append(Y)
		B = A
		A = term
		D = C
		C = Y

	return Y_array

def mp3_to_wav(name):
	sound = AudioSegment.from_mp3(name + ".mp3")
	sound.export(name + ".wav", format="wav")

def hpf(fs, original, fc):
	ret = lpf(0, fc, fs, original)
	index = 0
	Y_array = []
	for org in tqdm(original, unit =" sample", desc ="High Passing... "):
		Y_array.append(org - ret[index])
		index += 1
	return Y_array


if __name__ == "__main__":
	alt_kesme = input("Enter lower bound: ")
	ust_kesme = input("Enter upper bound: ")
	file_name = input("Enter file name: ")

	name = file_name.split(".")[0]
	ex = file_name.split(".")[1]

	fs, data = wavfile.read(file_name)
	print(file_name + " readed")

	ret = lpf(0, alt_kesme, fs, data)
	out_l = name + "_LPF" + ex
	arr = np.asarray(ret, dtype=np.int16)
	print(out_l + " has created")

	out_h = name + str(alt_kesme) + "Hz_" + str(ust_kesme) + "Hz.wav"
	ret = hpf(fs, arr, ust_kesme)
	arr = np.asarray(ret, dtype=np.int16)
	wavf.write(out_h, fs, arr)
	print(out_h + " has saved")

	# sound = AudioSegment.from_wav(out_h)
	# sound.export('myfile.mp3', format='mp3')
	# print("mp3 format saved")