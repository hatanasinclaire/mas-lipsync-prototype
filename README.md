# mas-lipsync-prototype

![example gif](https://cdn.discordapp.com/attachments/836882465599389756/1018422350624084038/lipsync4.gif)

![image](https://user-images.githubusercontent.com/96905447/189517964-b7736874-7999-45ab-87bd-91af4f21997f.png)

<h2>Overview</h2>

This an automated system designed specifically to automatically determines a sequence of face shapes ("_visemes_") from Monika's dialogue. The idea behind this system is that the **face shapes do not have to be specified manually for each line of dialogue**, and therefore does not require changing tens of thousands of lines of existing dialogue code.

This system performs a series of steps to convert text to facial shapes:

- The line is regexed to remove things like timing information. Numbers are converted to text using `num2words` and some punctuation is stripped out.
- The regexed line is converted into its English pronunciation. Pronunciation in English is often represented using the **International Phonetic Alphabet** (IPA), a standardized system used to describe sounds in human speech. The system uses `eng-to-ipa`'s `convert()` function to convert the text to the IPA representation of how it is pronounced.
- Because letters do not correspond directly to sounds in the English language, `eng-to-ipa` cannot catch the pronunciation of every word. A secondary function is used to manually specify pronunciation for some of the words that `eng-to-ipa` does not recognize. Failing this, the word is skipped if no pronunciation is available.
- The IPA pronunciation of the line is converted into the appropriate facial shapes using a lookup table. Though there are around 40-50 different sounds ("_phonemes_") commonly used in English, there are only half as many different facial shapes ("_visemes_") as some sounds will make the same shape. For example, the mouth makes the same shape when pronouncing _cat_ and _cut_.

I identify nineteen distinct mouth shapes corresponding to fifty phonemes. Brand new mouth sprites for these are included.

You can find more information on this prototype [here](https://github.com/Monika-After-Story/MonikaModDev/issues/9509).

<h2>How to use</h2> 
Two python files are included. `lipsync.py` contains only the mechanism, and `demo.py` is a file you can run to preview how the system works on some arbitrary input. You will have to run the demo from command line; just type `python demo.py` and it should run automatically off of the input text. 

You can copy-paste the dialogue label you want to test from a script `.rpy` straight into `input.txt`. The demo program should ignore things like tabs, exp codes, and non-dialogue lines so you don't have to worry about trimming them out. 

<h2>Requirements</h2>

`re`, `eng-to-ipa`, and `num2words` are needed for the actual mechanism of the system.

`pygame` is required solely for running the preview demo. 
