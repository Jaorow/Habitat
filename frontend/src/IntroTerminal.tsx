import {
  Terminal,
  TypingAnimation,
  AnimatedSpan,
} from '@/components/ui/shadcn-io/terminal';


const IntroTerminal = () => (
  <Terminal>
    <AnimatedSpan delay={0}>
      {`
                    _   _    ___  ____   _____        __
    ,_,            | | / \\  / _ \\|  _ \\ / _ \\ \\      / /
   (O,O)        _  | |/ _ \\| | | | |_) | | | \\ \\ /\\ / / 
   (   )       | |_| / ___ \\ |_| |  _ <| |_| |\\ V  V /  
  --"-"------   \\___/_/   \\_\\___/|_| \\_\\\\___/  \\_/\\_/   
      `}
    </AnimatedSpan>
    <AnimatedSpan delay={0}>$ Initialising Jaorow.com</AnimatedSpan>
    <TypingAnimation delay={1000} duration={70}>
      Initializing environment...
    </TypingAnimation>
    <AnimatedSpan delay={2500}>✓ Environment ready</AnimatedSpan>
    <TypingAnimation delay={3000} duration={70}>
      Loading modules...
    </TypingAnimation>
    <AnimatedSpan delay={4500}>✓ Modules loaded</AnimatedSpan>
    <TypingAnimation delay={5000} duration={90}>
      Starting application...
    </TypingAnimation>
    {/* <AnimatedSpan delay={6700}>🚀 All systems go. Ready to rock and Roll!</AnimatedSpan> */}
    <AnimatedSpan delay={6700} style={{ color: 'red', fontWeight: 'bold', display: 'inline-flex', alignItems: 'center' }}>
      🚧 Site is a work in progress. Come back later! 🚧
    </AnimatedSpan>
  </Terminal>
);
export default IntroTerminal;