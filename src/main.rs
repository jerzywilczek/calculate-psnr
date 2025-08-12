use std::num::NonZeroU32;
use std::io::{Read, Write};

fn main() {
    let args = std::env::args().collect::<Vec<_>>();

    if args.len() != 7 {
        println!(
            "usage: {} input.nv12 output.nv12 width height avg_bitrate max_bitrate",
            args[0]
        );
        return;
    }

    let input = &args[1];
    let output = &args[2];
    let width = args[3].parse::<NonZeroU32>().unwrap();
    let height = args[4].parse::<NonZeroU32>().unwrap();
    let avg_bigrate = args[5].parse::<u64>().unwrap();
    let max_bitrate = args[6].parse::<u64>().unwrap();

    let mut input = std::fs::File::open(input).unwrap();
    let mut output = std::fs::File::create(output).unwrap();

    let instance = vk_video::VulkanInstance::new().unwrap();
    let device = instance
        .create_device(Default::default(), Default::default(), None)
        .unwrap();

    let mut encoder = device
        .create_bytes_encoder(device.encoder_parameters_high_quality(
            vk_video::VideoParameters {
                width,
                height,
                target_framerate: vk_video::Rational {
                    numerator: 30,
                    denominator: NonZeroU32::new(1).unwrap(),
                },
            },
            vk_video::RateControl::Vbr {
                average_bitrate: avg_bigrate,
                max_bitrate: max_bitrate,
            },
        ))
        .unwrap();

    let mut decoder = device.create_bytes_decoder().unwrap();

    let frame_size = width.get() as usize * height.get() as usize * 3/2;
    let mut frame = vk_video::Frame { data: vk_video::RawFrameData {
        width: width.get(),
        height: height.get(),
        frame: vec![0; frame_size],
    }, pts: None };

    while let Ok(()) = input.read_exact(&mut frame.data.frame) {
        let encoded = encoder.encode(&frame, false).unwrap();
        let decoded = decoder.decode(vk_video::EncodedChunk { data: &encoded.data, pts: None }).unwrap();

        for frame in decoded {
            output.write_all(&frame.data.frame).unwrap();
        }
    }

    let last_frames = decoder.flush();
    for frame in last_frames {
        output.write_all(&frame.data.frame).unwrap();
    }
}
