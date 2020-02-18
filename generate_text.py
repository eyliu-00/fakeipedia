import gpt_2_simple as gpt2
from datetime import datetime
import os

""" A class that generates fake Wikipedia entries given a prompt. """
class Text_Generator():

    def __init__(self, model_name='run1'):
        """ Load the pre-generated model. """

        # if not os.path.isdir(os.path.join("models", "124M")):
    	#        gpt2.download_gpt2(model_name="124M")

        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess)
        self.sess = sess

    def generate_entry(self, prompt, model=None, run='run1', n_samples = 1, top_k = 1, length=400):
        """
        Prints out n_samples entries from a given prompt.
        @param prompt The prompt, or fixed prefix of the output entry.
        @param n_samples The number of samples to generate
        @param top_k How many candidate samples to generate per output sample.
               Higher top_k usually means higher quality of output entries.
        @return None (the entries are printed to the console)
        """

        return gpt2.generate(self.sess, model_name=model, run_name=run, truncate="@@@",
            prefix=prompt, top_k=top_k, nsamples=n_samples, return_as_list=True,
            )[0]
