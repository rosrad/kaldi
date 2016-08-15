C = `stty size`.split[1].to_i
S = [0x2743].pack("U*")
a = {}
puts "\033[2J"
loop {
  a[rand(C)] = 0
  a.each {|x, o|
    a[x] += 1
    print "\033[#{o};#{x}H \033[#{a[x]};#{x}H#{S} \033[0;0H"
  }
  STDOUT.flush
  sleep 0.03
}
