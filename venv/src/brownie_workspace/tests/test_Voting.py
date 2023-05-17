import pytest
from brownie import Voting, accounts

@pytest.fixture
def voting():
    return accounts[0].deploy(Voting, [b'dali', b'hama', b'racem'])

def test_candidateList(voting, accounts): 
    voting.candidateList(16194843617176052229761388124960209974297443629047419030586824313007175953166)
    assert False, "Not yet implemented"

def test_getCandidateList(voting, accounts): 
    voting.getCandidateList()
    assert False, "Not yet implemented"

def test_totalVotesFor(voting, accounts): 
    voting.totalVotesFor(b'RQbkQmm')
    assert False, "Not yet implemented"

def test_validCandidate(voting, accounts): 
    voting.validCandidate(b'nWDdg')
    assert False, "Not yet implemented"

def test_voteForCandidate(voting, accounts): 
    voting.voteForCandidate(b'mPXAWNNc', {"from": accounts[0]})
    assert False, "Not yet implemented"

def test_votesReceived(voting, accounts): 
    voting.votesReceived(b'kNSBOa')
    assert False, "Not yet implemented"
