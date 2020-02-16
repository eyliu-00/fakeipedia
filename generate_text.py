import gpt_2_simple as gpt2
from datetime import datetime
import os

""" A class that generates fake Wikipedia entries given a prompt. """
class Text_Generator():

    def __init__(self, model_name='run1'):
        """ Load the pre-generated model. """

        if model_name == "124M":
            if not os.path.isdir(os.path.join("models", model_name)):
        	       gpt2.download_gpt2(model_name=model_name)

        sess = gpt2.start_tf_sess()
        self.model_name = model_name
        if model_name != "124M":
            gpt2.load_gpt2(sess, run_name=self.model_name)
        self.sess = sess

    def generate_entry(self, prompt, n_samples = 1, top_k = 1, length=1000):
        """
        Prints out n_samples entries from a given prompt.
        @param prompt The prompt, or fixed prefix of the output entry.
        @param n_samples The number of samples to generate
        @param top_k How many candidate samples to generate per output sample.
               Higher top_k usually means higher quality of output entries.
        @return None (the entries are printed to the console)
        """
        return gpt2.generate(self.sess, run_name=self.model_name, truncate="@@@",
            prefix=prompt, top_k=top_k, nsamples=n_samples, return_as_list=True,
            length=length)[0]
