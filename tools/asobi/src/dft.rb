# DFT and IDFT implemented in Ruby
# Ref: http://en.wikipedia.org/wiki/Discrete_Fourier_transform

class Complex
  def inspect
    "(#{real.round(3)}, #{imag.round(3)}j)"
  end
end

def dft(seq)
  (0...seq.size).map do |k|
    (0...seq.size).map do |n|
      exp = -2.0 * Math::PI * k * n / seq.size
      seq[n] * Complex(Math.cos(exp), Math.sin(exp))
    end.reduce{ |acc, el| acc + el }
  end
end

def idft(seq)
  (0...seq.size).map do |n|
    (0...seq.size).map do |k|
      exp = 2.0 * Math::PI * k * n / seq.size
      seq[k] * Complex(Math.cos(exp), Math.sin(exp))
    end.reduce{ |acc, el| acc + el } / seq.size
  end
end

input = [1, 1, 1, 1]
p input
p dft(input)
p idft(dft(input))
puts

input = [1, 2, 3, 4, 5, 6]
p input
p dft(input)
p idft(dft(input))
