

# Check if it is a valid MPEG header.
# The argument *header* is a 32-bit unsigned integer.
#
# Refer to:
# - eyed3/mp3/headers.py: isValidHeader
# - http://www.mp3-tech.org/programmer/frame_header.html
def is_valid_header(header)
  # Frame sync
  sync = (header >> 16)
  if sync & 0xffe0 != 0xffe0
    #STDERR.puts "invalid sync bits"
    return false
  end

  # MPEG Audio version ID
  version = (header >> 19) & 0x3
  if version == 1  # 1 is reserved
    #STDERR.puts "invalid mpeg version"
    return false
  end

  # Layer description
  layer = (header >> 17) & 0x3
  if layer == 0  # 0 is reserved
    #STDERR.puts "invalid mpeg layer"
    return false
  end

  # Bitrate index
  bitrate = (header >> 12) & 0xf
  if bitrate == 0 || bitrate == 0xf
    #STDERR.puts "invalid mpeg bitrate"
    return false
  end

  sample_rate = (header >> 10) & 0x3
  if sample_rate == 0x3
    #STDERR.puts "invalid mpeg sample rate"
    return false
  end

  return true
end

def find_next_header(data, offset=0)
  pos = offset
  while true
    char = data[pos]
    break if char.nil?  # eof

    if char.ord == 0xff
      headstr = data[pos...pos+4]
      headint = headstr.unpack('N').first
      break if headint.nil?  # eof

      if is_valid_header(headint)
        return [pos, headint, headstr]
      end
    end

    pos += 1
  end

  return [nil, nil, nil]
end

# find and print all headers.
def find_headers(filename)
  filesize = File.size(filename)
  data = File.read(filename)
  data.force_encoding "BINARY"

  offset = count = 0
  last_pos = last_headint = nil
  while true
    pos, headint, _ = find_next_header(data, offset)
    if pos.nil?  # eof
      if last_pos != nil
        puts "Frame #{count} @#{last_pos}: 0x#{last_headint.to_s(16)}," +
             " #{filesize-last_pos} bytes (#{last_pos}, #{filesize})"
      end
      break
    else
      offset = pos + 4
      count += 1

      if count > 1
        puts "Frame #{count-1} @#{last_pos}: 0x#{last_headint.to_s(16)}," +
             " #{pos-last_pos} bytes (#{last_pos}, #{pos})"
      end

      last_pos = pos
      last_headint = headint
    end
  end
end

find_headers ARGV[0]
