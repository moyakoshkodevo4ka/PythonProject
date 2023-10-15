require 'spec_helper'
 
describe command('python --version') do
  its(:stdout) { should match 'Python 3.10.12' }
end
 
describe command('pip --version') do
  its(:exit_status) { should eq 0 }
end
 
describe package('torch') do
  it { should be_installed.by('pip').with_version('2.1.0') }
end
 
describe package('torchvision') do
  it { should be_installed.by("pip").with_version('0.16.0') }
end
 
describe package('PyAutoGUI') do
  it { should be_installed.by('pip').with_version('0.9.54') }
end
 
describe package('pyperclip') do
  it { should be_installed.by('pip').with_version('1.8.2') }
end
 
describe package('selenium') do
  it { should be_installed.by('pip').with_version('4.14.0') }
end
 
describe package('undetected-chromedriver') do
  it { should be_installed.by('pip').with_version('3.5.3') }
end
 
describe package('requests') do
  it { should be_installed.by('pip').with_version('2.31.0') }
end
 
describe package('response') do
  it { should be_installed.by('pip').with_version('0.5.0') }
end
 
describe package('transformers') do
  it { should be_installed.by('pip').with_version('4.34.0') }
end
 
describe package('tokenizers') do
  it { should be_installed.by('pip').with_version('0.14.1') }
end
 
describe package('sentence-transformers') do
  it { should be_installed.by('pip').with_version('2.2.2') }
end
 
describe package('networkx') do
  it { should be_installed.by('pip').with_version('3.1') }
end
 
describe package('nltk') do
  it { should be_installed.by('pip').with_version('3.8.1') }
end
 
describe package('numpy') do
  it { should be_installed.by('pip').with_version('1.26.1') }
end
 
describe package('git') do
  it { should be_installed }
en
