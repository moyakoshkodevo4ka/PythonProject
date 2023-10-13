# require 'spec_helper'

describe command('python --version') do
    its(:stdout) { should match 'Python 3.8.16' }
end

describe command('pip --version') do
    its(:exit_status) { should eq 0 }
end

describe package('torch') do
    it { should be_installed.by('pip').with_version('2.0.1') }
end

describe package('torchvision') do
    it { should be_installed.by('pip').with_version('0.15.2') }
end

describe package('PyAutoGUI') do
    it { should be_installed.by('pip').with_version('0.9.54') }
end

describe package('pyperclip') do
    it { should be_installed.by('pip').with_version('1.8.2') }
end

describe package('selenium') do
    it { should be_installed.by('pip').with_version('4.12.0') }
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
    it { should be_installed.by('pip').with_version('4.33.3') }
end

describe package('tokenizers') do
    it { should be_installed.by('pip').with_version('0.13.3') }
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
    it { should be_installed.by('pip').with_version('1.24.4') }
end

describe package('git') do
    it { should be_installed }
end