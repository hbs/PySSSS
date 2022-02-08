# **WARNING**

Due to the sensitive nature of your seed phrase, and while the seed phrase is never entered fully during the process described below, all operations described below should be performed on a trusted computer.

It is highly recommended you use Tails on a secure laptop to perform the various steps.

The splitting and checking phases require that you perform one action per word of your seed phrase, **DO NOT PERFORM THOSE ACTIONS IN THE ORDER OF THE WORDS IN YOUR SEED PHRASE**, for example, if your seed phrase is:

```
artwork reward notice certain title oak demand balance gain pudding fish bracket
```

perform the actions for the words in a random order, such as:

```
oak bracket pudding artwork reward fish balance certain demand title notice gain
```

or in alphabetical order (assuming this is not the order in the seed phrase):

```
artwork balance bracket certain demand fish gain notice oak pudding reward title
```

This will ensure that even in the unlikely case your computer was compromised during the process, the attacker would not know the order of the words in your seed phrase and would need to brute force it.

Note that this is just an additional security measure which may give you a little more time to move your funds to a safer wallet, your seed phrase should nevertheless be considered compromised.

Be careful to write down the shares in the correct order though and to respect the order of the words within each share.

# Shamir Secret Sharing for existing BIP39 seed phrases

The `ssss.py` utility allows to split an existing BIP39 seed phrase into `N` shares, `K` of which are needed for recovery.

The splitting is performed using the Shamir Secret Sharing library `PySSSS`.

The utility performs three functions, *split*, *check* and *recover*, all three are described below.

# Split

When called with the following syntax:

```
python3 bip39/ssss.py

then the command

split N K
```

The `ssss` utility will display a set of `N` random shares for each BIP39 word.

For each word of your seed phrase, copy the `N` shares next to the word. You can use the provided PDF template to write down the word number of each share on pieces of paper you can then hide in safe places or hand out to trusted parties.

For added security, run the above command at least once before processing each word and **DO NOT PROCESS THE WORDS OF YOUR SEED PHRASE IN ORDER**. Also **DO NOT REUSE SHARES** if a word appears multiple times in your seed phrase.

For even more security, reboot your computer between runs.

You **MUST** use the same values of `N` and `K` for splitting all words.

Once you have written down the shares for your entire seed phrase, you may want to validate that you did not make any errors.

# Check and recover

When called with the syntax:

```
python3 bip39/ssss.py

then the command

recover SHARE1 SHARE2 ... SHAREN
```

Where each `SHAREX` is the space separated words or word indices of the share.

The `ssss` utility will then attempt to recover the initial BIP39 word by testing all combinations of the shares. The output should then be similar to:

```
[XXXX]  WORD  K/N
```

Where `XXXX` is the index of the word in the BIP39 word list (1-2028), `WORD` is the actual word, and `K` and `N` are the minimum values of `K` and `N` which can be used for recovering the word. If `WORD` doesn't match the expected word or if the values of `K` and `N` displayed do not match those you used in the `split` phase, it means you made a mistake when you wrote down the shares, you should then perform a `split` again for all words with an error.

Once you have checked the shares for all your words, you can distribute the shares.

When performing a recovery, the syntax is identical but instead of inputing `N` shares, you only need to use `K`. The output should then show `K/K` instead of `K/N`.

Checking that you wrote the shares correctly or recovering the original seed phrase are very sensitive operations as you need to input sufficient shares to recover the original word, therefore you should **NEVER** perform those operations in the order of your seed phrase words and you should ideally reboot your computer between words or use multiple safe computers.

# Enjoy

This tool was crafted with love in the hope that it could be useful to as many people as possible and that it would contribute to make crypto a safer place.

If that tool helped you in any way, please consider donating some Monero to the following address:

83FsyoWQ8bxgqyZ2eLbBVU3W3jNr3bEc8XUsTr8jsBEH89JmhyD35LgLCb3LLNBLgfegEVMXBLnSqM5t4z8S4pQcMYZCYim

Any amount would be appreciated!
