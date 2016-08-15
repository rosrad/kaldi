
# mdct.rb
# Modified Discrete Cosine Transform (MDCT)
# https://en.wikipedia.org/wiki/Modified_discrete_cosine_transform

class Float
  def inspect
    "#{round(3)}"
  end
end

def mdct(seq)
  _N = seq.size / 2
  (0..._N).map do |k|
    (0..._N*2).map do |n|
      seq[n]*Math.cos(Math::PI/_N*(n+0.5+_N*0.5)*(k+0.5))
    end.reduce(:+)
  end
end

def imdct(seq)
  _N = seq.size
  (0..._N*2).map do |n|
    (0..._N).map do |k|
      seq[k]*Math.cos(Math::PI/_N*(n+0.5+_N*0.5)*(k+0.5))
    end.reduce(:+) / _N
  end
end

# [..., sa[i] + sb[i], ...]
def seqadd(sa, sb)
  0.upto(sa.size-1).map do |i|
    sa[i] + sb[i]
  end
end

# [..., sa[i] - sb[i], ...]
def seqsub(sa, sb)
  0.upto(sa.size-1).map do |i|
    sa[i] - sb[i]
  end
end

xn = [1, 1, 1, 1]
yn = mdct(xn)
zn = imdct(yn)
dn = seqsub(zn, xn)
puts "xn: #{xn}"
puts "yn: #{yn}"
puts "zn: #{zn}"
puts "zn-xn: #{dn}"

puts "\n================ imdct(mdct(xn)) != xn\n\n"

xn = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
puts "xn: #{xn}"

y1 = mdct(xn[0...8])
y2 = mdct(xn[4...12])
y3 = mdct(xn[8...16])
puts "y1: #{y1}"
puts "y2: #{y2}"
puts "y3: #{y3}"

z1 = imdct(y1) + [0.0] * 8
z2 = [0.0] * 4 + imdct(y2) + [0.0] * 4
z3 = [0.0] * 8 + imdct(y3)

puts "z1: #{z1}"
puts "z2: #{z2}"
puts "z3: #{z3}"

zn = seqadd(seqadd(z1, z2), z3)
puts "zn: #{zn}"

dn = seqsub(zn, xn)
puts "zn-xn: #{dn}"
puts

puts "\n================ (imdct(mdct(x[0:2N])) + imdct(mdct(x[N:3N])))[N:2N] == xn[N:2N]\n\n"
