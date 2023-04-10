#include <iostream>
#include <string>
#include <fstream>
#include <algorithm>
#include <vector>

std::vector<std::string> splitPage(std::string& page, std::string& chapter, int qlen){
    std::vector<std::string> result;
    size_t start = page.find(chapter);
    while (start != std::string::npos) {
        start += chapter.length()+qlen;
        size_t end = page.find(chapter, start);
        if (end != std::string::npos) {
            result.push_back(page.substr(start, end - start));
        } else {
            result.push_back(page.substr(start));
        }
        start = page.find(chapter, end);
    }
    return result;
}

void combineFiles(const std::vector<std::string>& fileNames, const std::string& outputFileName) {
    std::ofstream outputFile(outputFileName);

    for (const std::string& fileName : fileNames) {
        
        std::ifstream inputFile(fileName);

        std::string line;
        while (std::getline(inputFile, line)) {
            outputFile << line << std::endl;
        }
        inputFile.close();
    }

    outputFile.close();
    std::cout << "combined properly";
}
int main(){
    /*
    std::string chapNum = "24.";
    int questionLen = 2;
    std::ifstream infile("page.txt");
    if (!infile.is_open()) {
        std::cerr << "worked.\n";
        return 1;
    }
    std::string input((std::istreambuf_iterator<char>(infile)),
                    std::istreambuf_iterator<char>());
    //std::cout << input;
    char toDelete = '';
    input.erase(std::remove(input.begin(), input.end(),toDelete),input.end());
    //std::cout << input;
    std::vector<std::string> outputs = splitPage(input, chapNum,questionLen);
    std::ofstream outfile("chem24.csv");
    if (outfile.is_open()) {
        for (std::string& output : outputs) {
            std::replace(output.begin(), output.end(), '\n', ' ');
            outfile << "\"" << output << "\", \"Chemistry\"\n";
        }
        outfile.close();
        std::cout << "worked.\n";
    } else {
        std::cerr << "didnt work.\n";
        return 1;
    }

    return 0;
    */
   std::vector<std::string> files = {"chem1.csv","chem2.csv","chem3.csv","chem4.csv","chem5.csv","chem6.csv","chem7.csv","chem8.csv","chem9.csv","chem10.csv","chem11.csv","chem12.csv","chem13.csv","chem14.csv","chem15.csv","chem16.csv","chem17.csv","chem18.csv","chem19.csv","chem20.csv","chem21.csv","chem22.csv","chem23.csv","chem24.csv"};
   std::string outputFileName = "Chemistry.csv";
   combineFiles(files, outputFileName);
}
