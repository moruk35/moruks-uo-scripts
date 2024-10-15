# Moruk's Vendor Gater Script

# This script automatically casts Gate Travel every -gateInterval/1000- seconds.
# It sends the specified chat lines and plays emotes every -chatInterval/1000- seconds.
# You need to set up a restock agent for the reagents required to cast Gate Travel and update the -restockAgentName- variable.
# If you want to use a runebook prepare it by setting the desired rune as default in your runebook before running the script

# Settings: Customize these to fit your needs!
target = Target.PromptTarget("Select a recall rune or a runebook with Default Rune Set", 37)  # Select the runebook or a recall rune
chatColor = 53  # Set the color of text for your lines (53 is yellow, 62 is green, 37 red)
firstRun = True  # Flag to send the initial message once
restockAgentName = "vendorgateregrestock"
gateInterval = 60000  # Gate every 60 seconds
chatInterval = 7500  # Say something every 7.5 seconds
totalGates = 0

# Lines and emotes before casting the gate
beforeGateLines = [
    "New vendor with lowest prices!",
    "Gate will be ready in a few seconds...",
    "Almost there, hold on!",
    "Get ready to spend those golds!"
]

beforeGateEmotes = ["hey", "cough", "sniff", "woohoo"]

# Lines and emotes after casting the gate
afterGateLines = [
    "Relics, Rares, Wearables, Decos, RDAs and many more!",
    "Everything is on sale now!",
    "Check out the best deals in Britannia!"
]

afterGateEmotes = ["bow", "yell", "whistle"]

gateOpenLine = "Gating now, thank you for your patience!"

# Function to cast gate
def castGate(totalGates):
    if Player.Mana < 40:
        Misc.Pause(750)
        Player.ChatSay(53, "Low on Mana. Meditating...")  # Inform the player that the character is meditating
        Player.UseSkill("Meditation")
        while Player.Mana < 40:
            Misc.Pause(1000)
    Spells.CastMagery("Gate Travel")
    Player.ChatSay(93, gateOpenLine)
    Target.WaitForTarget(60000, False)
    Target.TargetExecute(target)
    totalGates += 1
    return totalGates

# Function to send lines and play emotes
def sendLinesAndEmotes(lines, emotes):
    for i in range(len(lines)):
        Player.ChatSay(chatColor, lines[i])
        Player.ChatSay(chatColor, "[e " + emotes[i])
        Misc.Pause(chatInterval)

# Main loop
while True:
    if firstRun:
        Misc.SendMessage("Moruk wishes you good sales and great profits", 101)
        firstRun = False  # Ensure this message is only said once
        Player.ChatSay(chatColor, "bank")  # Ensure bankbox is open for restocking

    Restock.RunOnce(restockAgentName, Player.Bank.Serial, Player.Backpack.Serial, 650)  # Restock regs

    # First set of lines and emotes (before casting gate)
    sendLinesAndEmotes(beforeGateLines, beforeGateEmotes)
    
    # Cast the gate
    totalGates = castGate(totalGates)  # Cast Gate Travel
    Misc.SendMessage("Total Gates: " + str(totalGates), 101)

    # Second set of lines and emotes (after casting gate)
    sendLinesAndEmotes(afterGateLines, afterGateEmotes)

    # Check the pause duration after casting gate
    pauseTime = gateInterval - (7 * chatInterval + 5000)

    if pauseTime > 0:
        Misc.Pause(pauseTime)
    else:
        Misc.Pause(5000)

