import subprocess, re, time, sys, math

DOMAIN  = "skyseevideo.com"
GOOD_NS = re.compile(r"ns\d+\.worldnic\.com", re.I)
BAD_NS  = re.compile(r"hostgator", re.I)

WAIT_ART = r"""
  ********   **   **  **  **                            **   **   **                 
 **//////   /**  //  /** /**                           //   /**  //            ***** 
/**        ****** ** /** /**       ***     **  ******   ** ****** ** *******  **///**
/*********///**/ /** /** /**      //**  * /** //////** /**///**/ /**//**///**/**  /**
////////**  /**  /** /** /**       /** ***/**  ******* /**  /**  /** /**  /**//******
       /**  /**  /** /** /**       /****/**** **////** /**  /**  /** /**  /** /////**
 ********   //** /** *** ***       ***/ ///**//********/**  //** /** ***  /**  ***** 
////////     //  // /// ///       ///    ///  //////// //    //  // ///   //  /////  
"""

SUCCESS_ART = r"""
 ░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░░▒▓███████▓▒░▒▓███████▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░     ░▒▓█▓▒░   
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░        
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓██████▓▒░  ░▒▓██████▓▒░░▒▓██████▓▒░  
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░     ░▒▓█▓▒░ 
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░     ░▒▓█▓▒░ 
░▒▓███████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░▒▓███████▓▒░▒▓███████▓▒░  
"""

COLORS         = [31,32,33,34,35,36,91,92,93,94,95,96]
CHECK_INTERVAL = 180      # seconds
FRAME_DELAY    = 0.1      # seconds

def rainbow(txt, offset):
    out, col = [], 0
    for ch in txt:
        if ch == "\n":
            out.append(ch)
            col = 0
        else:
            if ch != " ":
                out.append(f"\033[{COLORS[(col + offset) % len(COLORS)]}m{ch}")
            else:
                out.append(ch)
            col += 1
    out.append("\033[0m")
    return "".join(out)

def glow(txt, step):
    g = int((math.sin(step * 0.15) + 1) * 80 + 95)  # 95–255
    return f"\033[38;2;0;{g};0;1m{txt}\033[0m"

clear = lambda t: "\033[H\033[J" + t

def good():
    out = subprocess.check_output(
        ["nslookup", "-type=ns", DOMAIN],
        text=True,
        stderr=subprocess.STDOUT,
    )
    return len(GOOD_NS.findall(out)) >= 2 and not BAD_NS.search(out)

last_check = 0
is_good    = good()
i          = 0

sys.stdout.write("\033[?25l")
try:
    while True:
        now = time.time()
        if not is_good and now - last_check >= CHECK_INTERVAL:
            is_good = good()
            last_check = now

        frame = glow(SUCCESS_ART, i) if is_good else rainbow(WAIT_ART, i)
        sys.stdout.write(clear(frame))
        sys.stdout.flush()

        i += 1
        time.sleep(FRAME_DELAY)
finally:
    sys.stdout.write("\033[?25h")
