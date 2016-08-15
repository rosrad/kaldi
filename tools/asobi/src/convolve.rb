def convolve(va, vb)
  raise ArgumentError, "empty vector" if va.empty? || vb.empty?

  vb = vb.reverse
  val = va.size
  vbl = vb.size

  res = [0] * (val + vbl - 1)

  va.each_with_index do |a, i|
    vb.each_with_index do |b, j|
      res[i + j] += a * b
    end
  end

  res
end

a = [1, 1, 1]
b = [5, 3, 1]
c = [1, 2, 3]
d = [1, 2, 3, 4]

p convolve(a, a)  # [1, 2, 3, 2, 1]
p convolve(b, c)  # [15, 19, 14, 5, 1]
p convolve(b, d)  # [20, 27, 23, 14, 5, 1]
p convolve(d, b)  # [1, 5, 14, 23, 27, 20]
