# Radix-2 FFT and IFFT implemented in Ruby
# Ref: http://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm

class Complex
  def inspect
    "(#{real.round(3)}, #{imag.round(3)}j)"
  end
end

# W(N) = exp{-2 * pi * k / N} for k in (0..N-1)
def wn(n)
  (0...n).map do |k|
    exp = -2.0 * Math::PI * k / n
    Complex(Math.cos(exp), Math.sin(exp))
  end
end

# reverse W(N) = exp{2 * pi * k / N} for k in (0..N-1)
def rwn(n)
  (0...n).map do |k|
    exp = 2.0 * Math::PI * k / n
    Complex(Math.cos(exp), Math.sin(exp))
  end
end

def fft(seq)
  # recursion base
  return seq if seq.size <= 1

  # separate odd and even indexed entries
  seq_even = []
  seq_odd = []
  (0...seq.size).map do |i|
    ((i % 2 == 0) ? seq_even : seq_odd) << seq[i]
  end

  # recurse down
  seq_even_fft = fft(seq_even)
  seq_odd_fft = fft(seq_odd)

  # coefficients for seq_odd_fft
  seq_wn = wn(seq.size)

  n2 = seq.size / 2
  (0...seq.size).map do |i|
    if i < n2
      seq_even_fft[i] + seq_wn[i] * seq_odd_fft[i]
    else
      i -= n2
      seq_even_fft[i] - seq_wn[i] * seq_odd_fft[i]
    end
  end
end

def ifftn(seq)
  # recursion base
  return seq if seq.size <= 1

  # separate odd and even indexed entries
  seq_even = []
  seq_odd = []
  (0...seq.size).map do |i|
    ((i % 2 == 0) ? seq_even : seq_odd) << seq[i]
  end

  # recurse down
  seq_even_ifftn = ifftn(seq_even)
  seq_odd_ifftn = ifftn(seq_odd)

  # coefficients for seq_odd_ifftn
  seq_wn = rwn(seq.size)

  n2 = seq.size / 2
  (0...seq.size).map do |i|
    if i < n2
      seq_even_ifftn[i] + seq_wn[i] * seq_odd_ifftn[i]
    else
      i -= n2
      seq_even_ifftn[i] - seq_wn[i] * seq_odd_ifftn[i]
    end
  end
end

def ifft(seq)
  ifftn(seq).map{ |x| x / seq.size }
end

input = [1, 1, 1, 1]
p input
p fft(input)
p ifft(fft(input))
puts

input = [1, 2, 3, 4, 5, 6, 7, 8]
p input
p fft(input)
p ifft(fft(input))
puts

input = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
p input
p fft(input)
p ifft(fft(input))
