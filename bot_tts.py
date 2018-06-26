import argparse

bot_lines = ["Hi, I'm PopBot. I'm here to help you deal with stress. Can you tell me a little bit about a recent event that is stressing you out?", "Ok. What is it about the situation that is making you feel stressed?", "I see how that can be stressful.", "I'm sorry.", "I want you to take a couple of minutes and write at least one positive aspect about this situation.", "Let me know when you are done.", "Good job finding a positive! Is there another positive you can find in this situation?", "That's ok! You found some positive to the situation!", "Woohoo! See, you can usually find positives even when in the most negative of situations.", "Positive thinking can be a good way to destress, making it easier to face challenges.", "Thank you for sharing with me. I hope I have been able to help. Have a nice day!"]
bot_backchannels = ["Um", "Hmmmmmmmm", "hm", "ummmmmm", "uh", "uuuuuhhhhhhhh", "uhhhhhhhhh", "ok", "alright", "do you have anything else you'd like to say?", "is there anything you want to add."]

# [START auth_cloud_explicit]
def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'backchannel-experiment-8f97eb28255b.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
# [END auth_cloud_explicit]

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='backchannel-experiment-8f97eb28255b.json'

def main():
	for num,line in enumerate(bot_lines):
		synthesize_text(line, num, False)
	for num,line in enumerate(bot_backchannels):
		synthesize_text(line, num, True)

def synthesize_text(text, num, backchannel):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    if backchannel:
    	output_string = 'output' + str(num) + '_backchannel' + '.mp3'
    else:
   		output_string = 'output' + str(num) + '.mp3'

    with open(output_string, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file ' + output_string)


if __name__ == "__main__":
	main()