from ffmpy import FFprobe


if __name__ == '__main__':



    probe = FFprobe(
        inputs = {r"f:\record - 21 December 2016 - 07-43-48 PM - 00000.avi": None,
                  },
        global_options = ('-of', 'json', '-show_streams', '-show_format'),
    )

    a, b = probe.run()
    print a
