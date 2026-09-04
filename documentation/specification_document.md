# The specification document
I belong to he Bachelor's program in Computer Science (TKT). The language of the project will be English

The core of the project will be the use of Markov chains for note sequence generation / music generation. 

I'll be using mainly Python for the project. When I get further in the project I may need to also use other languages but I'll inform of changes here.

I'm proficient in python and SQLite and I can peer-review project written in those languages.

The data structure that I'll be implementing in the project is a Markov chain that will be trained with monophonic midi data. The Markov chain will have one of the two state representations based on the training data. State A would have pitch (MIDI note number 0-127), duration (note duration as 16th note) and time_between_notes (4th note, 8th note etc.). But if the training data doesn't have any gaps between the notes the time_between_notes would be 0 and therefore a useless variable. Duration + time_between_notes are supposed to represent rhythm but if time_between_notes is 0 rhythm can be represented solely by duration and therefore State B would just be pitch + duration. So which will be in the end used, state A or state B will be chosen later on. 

I'm not really solving any concrete problem I'd say, I'm just making an application that takes in information and based on probabilities it gives off new information. 

The inputs that the program receives is 1. a midi file or a list of tuples that represent the Markov chain states (A or B whichever is chosen), 2. how many notes does the output have to be 3. how many Markov orders will be taken into account in the process 4. Key constraint, yes, no and if yes which key to constraint to. The midi file is the base of the input, output length defines how many notes will be generated, the amount of Markov orders is how many many states of the Markov chain will be considered in the prediction and key constraint will force to choose the state which is in the correct key above other states (even though those might be more probable) if key cannot be forced the algorithm will revert to normal choice. 

Sources that are intended to be used are the python music21 libraries and possibly the Nottingham dataset ( https://github.com/jukedeck/nottingham-dataset/blob/master/MIDI/ashover10.mid ) if it is useful. 

