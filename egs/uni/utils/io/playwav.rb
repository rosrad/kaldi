#!/usr/bin/env ruby

if ARGV.empty?
  STDERR.puts "Usage: #{$0} foo.wav"
  exit 1
end

file = File.open(ARGV[0], "rb")

## head

chunk_id = file.read(4)
puts "ChunkID: #{chunk_id}" 
raise "not a RIFF file" if chunk_id != "RIFF"

chunk_size = file.read(4).unpack("L")[0]
puts "ChunkSize: #{chunk_size}"

format = file.read(4)
puts "Format: #{format}"
raise "not a WAVE file" if format != "WAVE"

## subchunk1

subchunk_1_id = file.read(4)
puts "Subchunk1ID: #{subchunk_1_id}"
raise "unexpected subchunk_1_id" if subchunk_1_id != "fmt "

subchunk_1_size = file.read(4).unpack("L")[0]
puts "Subchunk1Size: #{subchunk_1_size}"
raise "subchunk_1_size too small" if subchunk_1_size < 16

subchunk_1_data = file.read(subchunk_1_size)

audio_format, num_channels, sample_rate, byte_rate, block_align,
  bits_per_sample = subchunk_1_data[0..15].unpack("SSLLSS")
puts "AudioFormat: #{audio_format} (#{audio_format == 1 ? 'PCM' : 'UNKNOWN'})"
puts "NumChannels: #{num_channels} (#{num_channels == 1 ? 'Mono' : 'Stereo'})"
puts "SampleRate: #{sample_rate} Hz"
puts "ByteRate: #{byte_rate} B/s"
puts "BlockAlign: #{block_align} B"
puts "BitsPerSample: #{bits_per_sample}"

## subchunk2

subchunk_2_id = file.read(4)
puts "Subchunk2ID: #{subchunk_2_id}"
raise "unexpected subchunk_2_id" if subchunk_2_id != "data"

subchunk_2_size = file.read(4).unpack("L")[0]
puts "Subchunk2Size: #{subchunk_2_size}"

puts "PCM data starts from: #{file.tell}"

## play pcm data
## gem install ruby-alsa

require 'alsa'

ALSA::PCM::Playback.open do |playback|
  playback.write do |length|
    file.read length
  end
end

# References:
# https://ccrma.stanford.edu/courses/422/projects/WaveFormat/
# http://www.digitalpreservation.gov/formats/fdd/fdd000001.shtml
# http://www.sonicspot.com/guide/wavefiles.html
# http://www.360doc.com/content/09/0213/10/72158_2530988.shtml
# http://projects.tryphon.eu/projects/ruby-alsa/wiki
